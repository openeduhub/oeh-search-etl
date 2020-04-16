from converter.pipelines import ProcessValuespacePipeline;

class ValuespaceHelper:
    @staticmethod
    def mimetypeToLearningResourceType(mimetype):
        if mimetype.startswith('video/'):
            return 'video'
        if mimetype.startswith('image/'):
            return 'image'
        if mimetype.startswith('audio/'):
            return 'audio'

        return None